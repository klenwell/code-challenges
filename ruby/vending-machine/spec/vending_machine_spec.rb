require_relative "../lib/vending_machine"

# rubocop: disable Metrics/BlockLength
RSpec.describe VendingMachine do
  def setup_machine(tray_code='A1', price=50, products=[:cheetohs], coin_rolls={})
    subject.update_tray_price(tray_code, price)
    subject.stock_tray(tray_code, products)
    subject.coin_sorter.load(coin_rolls)
  end

  context "when instantiated" do
    it "includes a coin sorter" do
      expect(subject).to respond_to(:coin_sorter)
    end

    it "includes a 4x4 grid of product trays" do
      expect(subject).to respond_to(:product_trays)
      expect(subject.product_trays.length).to equal(16)
      expect(subject.product_trays).to have_key('A1')
      expect(subject.product_trays).to have_key('D4')
    end

    it "includes a display for messages" do
      expect(subject).to have_attributes({ display: nil })
    end
  end

  describe "consumer interface" do
    describe '#insert_coin' do
      it { is_expected.to respond_to(:insert_coin).with(1).argument }

      context 'when a valid coin is inserted' do
        it 'returns the total amount deposited' do
          expect(subject.insert_coin(1)).to eq(1)
          expect(subject.insert_coin(1)).to eq(2)
          expect(subject.insert_coin(100)).to eq(102)
        end
      end

      context 'when an invalid coin is inserted' do
        it 'displays an error message' do
          expect { subject.insert_coin(:invalid) }.to change { subject.display }
            .from(nil)
            .to('Invalid coin: invalid.')
        end

        it 'returns the existing amount deposited' do
          expect(subject.insert_coin(1)).to eq(1)
          expect(subject.insert_coin(:invalid)).to eq(1)
        end
      end
    end

    describe '#select_product' do
      it { is_expected.to respond_to(:select_product).with(1).argument }

      before(:each) { setup_machine('A1', 100, [:cheetohs] * 4) }

      context 'when product is available' do
        context 'when sufficient payment is made' do
          before(:each) { subject.insert_coin(100) }

          context 'when a valid product code is entered' do
            before(:each) { @product, @change = subject.select_product('A1') }
            it { expect(@product).to eq(:cheetohs) }
            it { expect(@change).to be_empty }
          end

          context 'when an invalid product code is entered' do
            before(:each) { @product, @change = subject.select_product('ZZ') }

            it { expect(@product).to eq(nil) }
            it { expect(@change).to be_empty }
            it { expect(subject.display).to eq('Invalid product code: ZZ') }
          end
        end

        context 'when overpayment is made' do
          before(:each) do
            subject.insert_coin(100)
            subject.insert_coin(10)
            @product, @change = subject.select_product('A1')
          end

          it { expect(@product).to eq(:cheetohs) }
          it { expect(@change).to eq([10]) }
        end

        context 'when insufficient payment is made' do
          before(:each) do
            subject.insert_coin(50)
            @product, @change = subject.select_product('A1')
          end

          it { expect(@product).to be_nil }
          it { expect(@change).to be_empty }
          it { expect(subject.display).to eq('Please deposit 50p') }
        end

        context "when machine does not have enough change" do
          before(:each) do
            @funds_before = subject.coin_sorter.sum
            subject.insert_coin(200)
            @product, @change = subject.select_product('A1')
          end

          it { expect(@product).to be_nil }
          it { expect(@change).to eq([200]) }
          it { expect(subject.display).to eq('Insufficient change: 100') }
          it { expect(subject.coin_sorter.sum).to eq(@funds_before) }
        end
      end

      context 'when product is unavailable' do
        before(:each) do
          subject.product_trays['A1'].empty
          expect(subject.product_trays['A1']).to be_empty
          subject.insert_coin(100)
          @product, @change = subject.select_product('A1')
        end

        it { expect(@product).to eq(nil) }
        it { expect(@change).to be_empty }
        it { expect(subject.display).to eq('Product sold out: A1') }
      end
    end

    describe '#cancel_transaction' do
      it { is_expected.to respond_to(:cancel_transaction).with(0).arguments }

      before(:each) do
        setup_machine('A1', 100, [:cheetohs] * 4)
        subject.insert_coin(50)
        @product, @change = subject.cancel_transaction
      end

      it { expect(@product).to be_nil }
      it { expect(@change).to eq([50]) }

      it 'resets the amount deposited' do
        subject.insert_coin(50)
        subject.select_product('A1')
        expect(subject.display).to eq('Please deposit 50p')
      end
    end
  end

  describe "vendor interface" do
    before(:each) { setup_machine }

    describe '#stock_tray' do
      it { is_expected.to respond_to(:stock_tray).with(2).arguments }

      context 'when a valid tray is stocked' do
        it 'updates the tray contents' do
          # Arrange
          tray_b1 = subject.product_trays['B1']

          # Assume
          expect(tray_b1).to be_empty

          # Act
          slots = subject.stock_tray('B1', [:gum, :gum, :gum])

          # Assert
          expect(tray_b1).not_to be_empty
          expect(slots).to eq([:gum, :gum, :gum])
        end
      end

      context 'when an invalid tray is stocked' do
        it { expect { subject.stock_tray('ZZ', [:top]) }.to raise_error(NoMethodError) }
      end
    end

    describe '#update_tray_price' do
      it { is_expected.to respond_to(:update_tray_price).with(2).arguments }

      it 'updates tray price' do
        # Arrange
        price_before = subject.product_trays['A1'].price
        products_before = subject.product_trays['A1'].products

        # Assume
        expect(price_before).to eq(50)

        # Act
        new_price = subject.update_tray_price('A1', 100)

        # Assert
        expect(new_price).to eq(subject.product_trays['A1'].price)
        expect(subject.product_trays['A1'].price).to eq(100)
        expect(subject.product_trays['A1'].products).to eq(products_before)
      end
    end

    describe '#count_products' do
      it { is_expected.to respond_to(:count_products).with(0).arguments }

      it 'counts all products in machine' do
        # Arrange
        subject.stock_tray('A1', [:cheetohs, :cheetohs])
        subject.stock_tray('B1', [:doritos, :doritos, :doritos])
        subject.stock_tray('D4', [:cheetohs, :doritos])

        # Assume
        # A1 already had on bag of cheetohs
        expect(subject.product_trays['A1'].products).to eq({ cheetohs: 3 })

        # Act
        counts = subject.count_products

        # Assert
        expect(counts).to eq({ cheetohs: 4, doritos: 4 })
      end
    end

    describe '#status' do
      it { is_expected.to respond_to(:status).with(0).arguments }

      it 'outputs a report of products, coins, and total coin amount' do
        # Act
        report = subject.status

        # Assert
        expect(report).to match(/Products/)
        expect(report).to match(/Coins/)
        expect(report).to match(/Amount/)
      end
    end
  end
end
# rubocop: enable Metrics/BlockLength
