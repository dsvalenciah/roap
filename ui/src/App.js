import React from 'react'
import {
  BrowserRouter as Router,
  Route
} from 'react-router-dom'

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import sentences from './lang/index';
import NavigationBar from './components/NavigationBar';

const Main = () => (
  <Router>
    <MuiThemeProvider>
      <NavigationBar appName={ 'ROAp' }/>
      <Route
        exact
        path="/"
        render={ (props) => (<Home hi='hi' />) }
      />
      <Route path="/search" component={Search}/>
      <Route path="/new-users" component={NewUsers}/>
      <Route path="/reported-publications" component={ReportedPublications}/>
      <Route path="/languages" component={Languages}/>
      <Route path="/fonts" component={Fonts}/>
      <Route path="/sign-in" component={SignIn}/>
      <Route path="/sign-out" component={SignOut}/>
      <Route path="/profile" component={Profile}/>
    </MuiThemeProvider>
  </Router>
)

class Home extends React.Component {
  render() {
    return (
      <div>
        <h2>Home</h2>
        <h2>Active language: { sentences.getLanguage() }</h2>
        <h2>this is a prop: { this.props.hi }</h2>
      </div>
    )
  }
}

class Search extends React.Component {
  render() {
    return (
      <div>
        <h2>Search</h2>
      </div>
    )
  }
}

class NewUsers extends React.Component {
  render() {
    return (
      <div>
        <h2>NewUsers</h2>
      </div>
    )
  }
}

class ReportedPublications extends React.Component {
  render() {
    return (
      <div>
        <h2>ReportedPublications</h2>
      </div>
    )
  }
}

class Languages extends React.Component {
  render() {
    return (
      <div>
        <h2>Languages</h2>
      </div>
    )
  }
}

class Fonts extends React.Component {
  render() {
    return (
      <div>
        <h2>Fonts</h2>
      </div>
    )
  }
}

class SignIn extends React.Component {
  render() {
    return (
      <div>
        <h2>SignIn</h2>
      </div>
    )
  }
}

class SignOut extends React.Component {
  render() {
    return (
      <div>
        <h2>SignOut</h2>
      </div>
    )
  }
}

class Profile extends React.Component {
  render() {
    return (
      <div>
        <h2>Profile</h2>
      </div>
    )
  }
}

export default Main