import "cypress-file-upload";

describe("API Error Handling", () => {
    beforeEach(() => {
        cy.visit("http://127.0.0.1:5000");
    });

    it("Displays error message if translation fails", () => {
        // Intercept translation API call and simulate failure
        cy.intercept("POST", "/translate", {
            statusCode: 500,
            body: {error: "Translation failed"},
        });

        // Upload a file
        cy.get('input[type="file"]').attachFile({
                filePath: 'test.pdf',
                mimeType: 'application/pdf',
                encoding: "base64"
            },
            {
                force: true,
                uploadType: "input"
            })

        // Select language and submit
        cy.get('select[name="target_lang"]').select("French");
        cy.get('button[type="submit"]').click();

        // Verify error message is displayed
        cy.contains("Error: Translation failed").should("be.visible");
    });
});
