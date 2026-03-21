require "test_helper"

class RentalTest < ActiveSupport::TestCase
  test "emoji falls back to default" do
    rental = Rental.new(emoji_key: "unknown")

    assert_equal DUMPSTER_ICONS["default"], rental.emoji
  end

  test "emoji uses configured icon" do
    rental = Rental.new(emoji_key: "A")

    assert_equal DUMPSTER_ICONS["A"], rental.emoji
  end
end
