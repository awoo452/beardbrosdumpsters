require "application_system_test_case"

class RentalsTest < ApplicationSystemTestCase
  setup do
    @rental = rentals(:one)
    @user = users(:one)
    sign_in @user
  end

  test "visiting the index" do
    visit rentals_url
    assert_selector "h1", text: "Dumpster Rental Calendar"
  end

  test "should create rental" do
    visit dashboard_url
    click_on "New Rental"

    new_title = "New Rental"
    fill_in "Title", with: new_title
    fill_in "Address", with: "123 Test Street"
    fill_in "Start time", with: @rental.start_time.strftime("%Y-%m-%dT%H:%M")
    fill_in "End time", with: @rental.end_time.strftime("%Y-%m-%dT%H:%M")
    click_on "Create Rental"

    assert_text new_title
  end

  test "should update Rental" do
    visit rental_url(@rental)
    click_on "Edit this rental", match: :first

    updated_title = "Updated Rental"
    fill_in "Title", with: updated_title
    fill_in "Address", with: "456 Updated Street"
    fill_in "Start time", with: @rental.start_time.strftime("%Y-%m-%dT%H:%M")
    fill_in "End time", with: @rental.end_time.strftime("%Y-%m-%dT%H:%M")
    click_on "Update Rental"

    assert_text updated_title
  end

  test "should destroy Rental" do
    visit rental_url(@rental)
    click_on "Destroy this rental", match: :first

    assert_current_path rentals_path
  end
end
