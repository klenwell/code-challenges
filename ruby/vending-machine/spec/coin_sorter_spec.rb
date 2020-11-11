require_relative "../lib/vending_machine/coin_sorter"

RSpec.describe CoinSorter do
  describe '.new' do
  end

  describe '#deposit' do
    it { is_expected.to respond_to(:deposit).with(1).arguments }

    context 'when coin is valid' do
      it { expect(subject.deposit(10)).to eq(10) }
    end

    context 'when coin is invalid' do
      it { expect { subject.deposit(3) }.to raise_error(described_class::InvalidCoinError) }
    end
  end

  describe '#load' do; end

  describe '#roll' do; end

  describe '#make_change' do; end

  describe '#inventory' do; end

  describe '#total' do; end
end
