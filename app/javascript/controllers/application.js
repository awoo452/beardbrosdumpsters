import { Application } from "@hotwired/stimulus"

// Start the Stimulus application
const application = Application.start()

// Disable debug mode for production
application.debug = false

// Expose Stimulus application globally for debugging
window.Stimulus = application

export { application }
