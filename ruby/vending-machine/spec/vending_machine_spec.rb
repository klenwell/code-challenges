require_relative "../lib/vending_machine"

RSpec.describe VendingMachine do
  describe "when first created" do
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
end
