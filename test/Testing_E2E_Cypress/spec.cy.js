var target = 'http://sonardom.ddns.net:12020/cypress'
describe('test iniziale', () => {
  //controllo attività del dominio
  it('accessibilità', () => {
    cy.visit(target)
  })

  //controllo presenza modalità di gioco nella pagina iniziale
  it('contiene varianti', () => {
    cy.visit(target)
    cy.contains('GIOCA') //è case sensitive
    cy.contains('uniMOREchess')
    cy.contains('Crazy House')
    cy.contains('Quadriglia')
  })

  //controllo funzionamento modalità classica
  it('contiene elemtenti di app', () => {
    cy.visit(target)
    //caricamento storia delle mosse
    cy.contains('Crazy House').click()
    //cy.url().should('include','/cypress/gioca')
    cy.get('body').then($body => {
      //l'app è caricata
      $body.find('#app')
      //è presente la storia
      $body.find('#moveTable')
      //è presente la scacchiera
      $body.find('main-board')
      //è presente la chat
      $body.find('chatbox')
    })  
  })
  it('controllo chat modalità classica', () => {
    //accesso pagina di gioco
    cy.visit(target)
    cy.contains('GIOCA').click()

    //interazione con chat
    cy.get('input[type=text]').type('test messaggio')
    //invio messaggio
    cy.contains('Send').click()
    //controllo invio
    cy.contains('test messaggio')

    cy.get('input[type=text]').type('test risposta')
    //invio messaggio
    cy.contains('Send').click()
    //controllo invio
    cy.contains('test risposta')
  })
})
