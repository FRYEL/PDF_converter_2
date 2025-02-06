const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:5000", // Adjust to your Flask server's URL
    supportFile: false,
  },
});
