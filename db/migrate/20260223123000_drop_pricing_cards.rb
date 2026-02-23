class DropPricingCards < ActiveRecord::Migration[7.1]
  def change
    drop_table :pricing_cards, if_exists: true
  end
end
