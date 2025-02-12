import "cypress-file-upload";

describe("PDF Translator and Summarizer", () => {
  beforeEach(() => {
    cy.visit("http://127.0.0.1:5000/");
  });

  it("Uploads a PDF and processes it", () => {
    // Upload a PDF
    cy.get('input[type="file"]').attachFile({
                filePath: 'test.pdf',
                mimeType: 'application/pdf',
                encoding: "base64"
            },
            {
                force: true,
                uploadType: "input"
            })

    // Select a target language
    cy.get('select[name="target_lang"]').select("German");

    // Submit the form
    cy.get('button[type="submit"]').click();

    // Verify results
    cy.get("#loading-overlay").should("be.visible");
    cy.get("#results", {timeout: 15000}).should("be.visible");
    cy.get("#translated-text").should("not.be.empty");
  });
});
