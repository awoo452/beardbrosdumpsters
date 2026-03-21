require "application_system_test_case"

class LandingCardsTest < ApplicationSystemTestCase
  setup do
    @landing_card = landing_cards(:one)
    @user = users(:one)
    sign_in @user
  end

  test "visiting the index" do
    visit landing_cards_url
    assert_selector "h1", text: "Landing cards"
  end

  test "should create landing card" do
    visit landing_cards_url
    click_on "New landing card"

    new_title = "New Landing Card"
    fill_in "Title", with: new_title
    fill_in "Description", with: "Landing card description"
    fill_in "Image", with: ""
    click_on "Create Landing card"

    assert_text new_title
  end

  test "should update Landing card" do
    visit landing_card_url(@landing_card)
    click_on "Edit this landing card", match: :first

    updated_title = "Updated Landing Card"
    fill_in "Title", with: updated_title
    fill_in "Description", with: "Updated description"
    fill_in "Image", with: ""
    click_on "Update Landing card"

    assert_text updated_title
  end

  test "should destroy Landing card" do
    visit landing_card_url(@landing_card)
    click_on "Destroy this landing card", match: :first

    assert_current_path landing_cards_path
  end
end
