require "application_system_test_case"

class VideosTest < ApplicationSystemTestCase
  setup do
    @video = videos(:one)
    @user = users(:one)
    sign_in @user
  end

  test "visiting the index" do
    visit videos_url
    assert_selector "h2", text: "Videos"
  end

  test "should create video" do
    visit dashboard_url
    click_on "New Video"

    new_title = "New Video"
    fill_in "Title", with: new_title
    fill_in "Description", with: "New video description"
    fill_in "Youtube", with: "abc123"
    click_on "Create Video"

    assert_text new_title
  end

  test "should update Video" do
    visit video_url(@video)
    click_on "Edit this video", match: :first

    updated_title = "Updated Video"
    fill_in "Title", with: updated_title
    fill_in "Description", with: "Updated description"
    fill_in "Youtube", with: "xyz789"
    click_on "Update Video"

    assert_text updated_title
  end

  test "should destroy Video" do
    visit video_url(@video)
    click_on "Destroy this video", match: :first

    assert_current_path videos_path
  end
end
