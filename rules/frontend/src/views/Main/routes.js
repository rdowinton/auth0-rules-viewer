import React from 'react'
import {Route, IndexRedirect} from 'react-router'
import AuthService from 'utils/AuthService'
import Container from './Container'
import Login from './Login/Login'
import Rules from './Rules/Rules'

const auth = new AuthService("Your client ID", "Your domain");

// onEnter callback to validate authentication in private routes
const requireAuth = (nextState, replace) => {
  if (!auth.loggedIn()) {
    replace({ pathname: '/login' })
  }
}

export const makeMainRoutes = () => {
  return (
    <Route path="/" component={Container} auth={auth}>
      <IndexRedirect to="/rules" />
      <Route path="rules" component={Rules} onEnter={requireAuth} />
      <Route path="login" component={Login} />
    </Route>
  )
}

export default makeMainRoutes
