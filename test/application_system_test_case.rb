require "test_helper"

class ApplicationSystemTestCase < ActionDispatch::SystemTestCase
  if ENV["CI"]
    driven_by :rack_test
  else
    driven_by :selenium, using: :chrome, screen_size: [1400, 1400]
  end
end
