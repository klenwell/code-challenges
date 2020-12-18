require 'spec_helper'
require_relative '../../app/models/household'


describe Household, type: :model do
  it { is_expected.to be_a(Household) }
end
