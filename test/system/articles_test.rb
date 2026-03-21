require "application_system_test_case"

class ArticlesTest < ApplicationSystemTestCase
  setup do
    @article = articles(:one)
    @user = users(:one)
    sign_in @user
  end

  test "visiting the index" do
    visit articles_url
    assert_selector "h1", text: @article.title
  end

  test "should create article" do
    visit dashboard_url
    click_on "New Article"

    new_title = "New Article Title"
    fill_in "Title", with: new_title
    fill_in "Description", with: "New article description"
    fill_in "Body", with: "New article body"
    fill_in "Image", with: ""
    click_on "Create Article"

    assert_text new_title
  end

  test "should update Article" do
    visit article_url(@article)
    click_on "Edit this article", match: :first

    updated_title = "Updated Article Title"
    fill_in "Title", with: updated_title
    fill_in "Description", with: "Updated description"
    fill_in "Body", with: "Updated body"
    fill_in "Image", with: ""
    click_on "Update Article"

    assert_text updated_title
  end

  test "should destroy Article" do
    visit article_url(@article)
    click_on "Destroy this article", match: :first

    assert_current_path articles_path
  end
end
