/**
 * Cypress UI Functionality end-to-end (e2e) test case:
 * Who: I wrote this.
 * What: Test case is written for a website (private repo) 
 * When: September 22, 2022
 * Why: This e2e test case was necessary for checking one of the basic UI 
 * functionalities of the website I started building 
 * (not deployed yet as of Feb. 17, 2023)
 * 
 * NOTE: Don't try forking and running this file. This repo does not have cypress installed. 
 * This is just a snippet of what I know about e2e testing.
 * 
 * 
 * -------------------
 * Thought Process of this Test Case: 
 * -------------------
 * This test case should reveal the text associated to its 
 * corresponding button when the user is hovering their mouse over that button. 
 * 1.) Cypress will first go to the local dev environment that I linked it to (localhost:3000)
 * 2.) For each element that has class '.sidebarbuttons'
 *      ... create a let variable called buttonText
 *      ... create a variable called 'normalizeText' that holds the functionality of removing 
 *          all white space characters with an empty '', and lower-case the button value text.
 *      ... wrap the iterated element to yield the element to be triggered with a mouseover
 *      
 *      2a.) Check button text value:
 *      ... Upon mouseover, check that the button has a text (w/ a data type that's a string)
 *          ... call normalizeText and feed in the corresponding text of the button as the argument.
 *      2b.) Check button span value
 *      ... Upon mouseover, check that the button has a span (w/ a data type that's a string)
 *          ... check that the span text equals to the button text from part A.)
 *      2c.) Check button span visibility
 *      ... Upon mouseover, the element with span tag should be visible
 *      ... Upon mouseleave, the element with span tag should be hidden
 * 
 */

describe('Website UI Functionality', () => {
    it('Reveal/conveal the text of the button on mouseover/mouseleave', () => {
        cy.visit('http://localhost:3000')
        cy.get('.sidebarbuttons').each((el) => {
          let buttonText;
          const normalizeText = (s) => s.replace(/\s/g, '').toLowerCase();
          cy.wrap(el).trigger('mouseover')
          // check button value
          cy.contains('button', el.val().toString())
            .then(($sidebarButtonValue) => {
              buttonText= normalizeText($sidebarButtonValue.text());
            }) 
          // check span value 
          cy.contains('span', el.val().toString())
            .should(($spanText) => {
              const spanText = normalizeText($spanText.text())
              expect(spanText).to.equal(buttonText)
            }) 
          cy.get('span').should('be.visible')
          cy.wrap(el).trigger('mouseleave')
          cy.get('span').should('be.hidden')
        })
      });
})