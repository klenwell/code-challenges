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

    describe '#update_tray_price' do; end

    describe '#count_products' do; end

    describe '#status' do; end
  end

  context "as a vendor using interface" do
    before(:each) do
      subject.stock_tray('A1', [:cheetohs] * 4)
      subject.stock_tray('D4', [:doritos] * 4)
      subject.coin_sorter.load({ 1 => 50, 2 => 20, 5 => 2 })
    end

    it "expects an initial load of products" do
      expect(subject.count_products[:cheetohs]).to equal(4)
      expect(subject.count_products[:doritos]).to equal(4)
    end

    it "expects to reload change" do
      # Assume
      expect(subject.coin_sorter.select(1)).to equal(50)
      expect(subject.coin_sorter.select(100)).to equal(0)
      expect(subject.coin_sorter.sum).to equal(100)

      # Act
      subject.coin_sorter.load({ 1 => 50, 100 => 1 })

      # Assert
      expect(subject.coin_sorter.select(1)).to equal(100)
      expect(subject.coin_sorter.select(100)).to equal(1)
      expect(subject.coin_sorter.sum).to equal(250)
    end

    it "expects to update price of product tray" do
      # Arrange
      tray_a1 = subject.product_trays['A1']
      new_tray_price = 25

      # Assume
      expect(described_class::INIT_PRICES).to include(tray_a1.price)
      expect(tray_a1.price).not_to equal(new_tray_price)

      # Act
      subject.update_tray_price('A1', new_tray_price)

      # Assert
      expect(tray_a1.price).to equal(new_tray_price)
    end

    it "expects to keep track of products" do
      expect(subject.count_products[:cheetohs]).to equal(4)
      expect(subject.count_products[:doritos]).to equal(4)
    end

    it "expects to keep track of change" do
      expect(subject.coin_sorter.select(1)).to equal(50)
      expect(subject.coin_sorter.select(100)).to equal(0)
      expect(subject.coin_sorter.sum).to equal(100)
    end
  end
end
# rubocop: enable Metrics/BlockLength
