require "test_helper"

class UserTest < ActiveSupport::TestCase
  test "approved users are active" do
    user = users(:one)

    assert user.active_for_authentication?
  end

  test "unapproved users are inactive" do
    user = users(:two)

    assert_not user.active_for_authentication?
  end
end
