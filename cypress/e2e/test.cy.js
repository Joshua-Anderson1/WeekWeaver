describe('Sample Test', () => {
    it('Sample Test to visit home page', () => {
        cy.wait(500);
        cy.visit('/');
        cy.wait(500);
        cy.contains('Sign in');
        cy.contains('Sign up');
        cy.contains('About');
        cy.contains('Team');
    });
});
describe('Create and See a Task Successfully', () => {
    it("Can Log In", () => {
        cy.wait(500);
        cy.visit('/');
        cy.wait(500);

        //Log In successfully
        cy.visit('/accounts/login/');
        cy.get('input[name="username"]').type("test@gmail.com");
        cy.get('input[name="password"]').type("jFgAYCip8HXnUUg");
        cy.get('button[type="submit"]').click();
        cy.wait(500);
        //Add Task successfully
        cy.visit('/tasks/add');
        cy.get('input[name="task_name"]').type("Test Task");
        cy.get('input[name="task_deadline"]').type("2024-10-29");
        cy.get('button[type="submit"]').click();
          cy.get('input[name="how_much_prep"]').type("A bit");
          it('should click the submit button', { retries: 0 }, () => {
            cy.get('button[type="submit"]').click({ force: true, multiple: true });
          });
          cy.wait(500);

          cy.visit('/tasks');
      });
});

describe('Create and See a Calendar Successfully', () => {
    it("Can Log In", () => {
        cy.wait(500);
        cy.visit('/');
        cy.wait(500);
        //Go through the login process
        cy.visit('/accounts/login/');
        cy.get('input[name="username"]').type("test@gmail.com");
        cy.get('input[name="password"]').type("jFgAYCip8HXnUUg");
        cy.get('button[type="submit"]').click();
        cy.wait(500);
        //Add a calendar successfully
        cy.visit('/calendar/add');
        cy.get('input[name="calendar_name"]').type("Test Calendar");
        cy.get('input[name="notifications"]').type("This assignment is due soon.");
        cy.get('button[type="submit"]').click();
        cy.wait(500);
      });
});