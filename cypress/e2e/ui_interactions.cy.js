import "cypress-file-upload";

describe("UI Interactions", () => {
    beforeEach(() => {
        cy.visit("http://127.0.0.1:5000");
    });

    it("Shows a loading spinner while processing", () => {
        cy.get('input[type="file"]').attachFile({
                filePath: 'test.pdf',
                mimeType: 'application/pdf',
                encoding: "base64"
            },
            {
                force: true,
                uploadType: "input"
            })
        cy.wait(2000); // Wait for processing to start
        cy.get('select[name="target_lang"]').select("Spanish");
        cy.wait(2000); // Wait for processing to start
        cy.get('button[type="submit"]').click();
        cy.wait(2000); // Wait for processing to start
        cy.get('#loading-overlay').should('have.css', 'display', 'flex');
        // Check spinner appears
        cy.get('#loading-overlay', {timeout: 15000}).should('be.visible'); // Wait for spinner to appear

        // Spinner should disappear after processing
        cy.get('#loading-overlay',{timeout: 15000}).should('have.css', 'display', 'none');
    });

    it("Hides results section initially", () => {
        cy.get("#results").should("have.class", "hidden");
    });
});
