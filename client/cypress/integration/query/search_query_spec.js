describe('Search Query', () => {
  beforeEach(() => {
    cy.login();

    cy.request('POST', 'api/queries', {
      name: '用户数量',
      data_source_id: 1,
      query: 'SELECT 1',
    });

    cy.request('POST', 'api/queries', {
      name: '模型数量',
      data_source_id: 1,
      query: 'SELECT 1',
    });

    cy.visit('/');
  });

  it('finds queries by name', () => {
    cy.getByTestId('AppHeaderSearch').type('Users{enter}');
    cy.contains('Users Count');
  });
});