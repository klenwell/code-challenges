require_relative "../lib/vending_machine"

RSpec.describe VendingMachine do
  context "when first created" do
    it "expects to include a coin sorter" do
      expect(subject).to respond_to(:coin_sorter)
    end

    it "expects a have 4x4 grid of product trays" do
      expect(subject).to respond_to(:product_trays)
      expect(subject.product_trays.length).to equal(16)
      expect(subject.product_trays).to have_key('A1')
      expect(subject.product_trays).to have_key('D4')
    end
  end

  context "as a consumer using interface" do
    it { is_expected.not_to respond_to(:insert_coin).with(0).argument }
    it { is_expected.to respond_to(:insert_coin).with(1).arguments }

    it { is_expected.not_to respond_to(:select_product).with(0).argument }
    it { is_expected.to respond_to(:select_product).with(1).arguments }

    it { is_expected.to respond_to(:cancel_transaction).with(0).argument }
    it { is_expected.not_to respond_to(:cancel_transaction).with(1).arguments }
  end

  context "as a vendor using interface" do
    before(:each) do
      subject.stock_tray('A1', [:cheetohs] * 4)
      subject.stock_tray('D4', [:doritos] * 4)
      subject.coin_sorter.load({1 => 50, 2 => 20, 5 => 2})
    end

    it "expects an initial load of products" do
      expect(subject.product_counts[:cheetohs]).to equal(4)
      expect(subject.product_counts[:doritos]).to equal(4)
    end

    it "expects to reload change" do
      # Assume
      expect(subject.coin_sorter.inventory(1)).to equal(50)
      expect(subject.coin_sorter.inventory(100)).to equal(0)
      expect(subject.coin_sorter.total).to equal(100)

      # Act
      subject.coin_sorter.load({1 => 50, 100 => 1})

      # Assert
      expect(subject.coin_sorter.inventory(1)).to equal(100)
      expect(subject.coin_sorter.inventory(100)).to equal(1)
      expect(subject.coin_sorter.total).to equal(250)
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
      expect(subject.product_counts[:cheetohs]).to equal(4)
      expect(subject.product_counts[:doritos]).to equal(4)
    end

    it "expects to keep track ofchange" do
      expect(subject.coin_sorter.inventory(1)).to equal(50)
      expect(subject.coin_sorter.inventory(100)).to equal(0)
      expect(subject.coin_sorter.total).to equal(100)
    end
  end

  context "when product is selected and appropriate money is inserted" do
    it "expects to receive product without change" do
      # Arrange
      subject.stock_tray('A1', [:cheetohs] * 4)
      subject.update_tray_price('A1', 100)

      # Assume
      expect(subject.product_counts[:cheetohs]).to equal(4)
      expect(subject.coin_sorter.total).to equal(0)

      # Act
      subject.insert_coin(100)
      product, change = subject.select_product('A1')

      # Arrange
      expect(product).to equal(:cheetohs)
      expect(change).to be_empty
      expect(subject.product_counts[:cheetohs]).to equal(3)
      expect(subject.coin_sorter.total).to equal(100)
    end
  end

  context "when too much money is inserted for product" do
  end

  context "when insufficient funds have been inserted for product" do
  end

  context "when wrong product code is entered" do; end

  context "when machine does not have enough change" do; end

  context "when machine is out of requested product" do; end
end
