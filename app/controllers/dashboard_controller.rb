class DashboardController < ApplicationController
  before_action :authenticate_user!
  before_action :check_approval

  def index
    @user = current_user
    @landing_cards = LandingCard.all
    @articles = Article.all
    @rentals = Rental.all
    @videos = Video.all
  end

  private

  def check_approval
    unless current_user.approved?
      redirect_to root_path
    end
  end
end
