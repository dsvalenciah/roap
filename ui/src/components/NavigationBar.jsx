import React from 'react'
import PropTypes from 'prop-types'

import {Link, withRouter} from 'react-router-dom'

import AppBar  from 'material-ui/AppBar'
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
import SocialPerson from 'material-ui/svg-icons/social/person';
import Settings from 'material-ui/svg-icons/action/settings';
import FindInPage from 'material-ui/svg-icons/action/find-in-page';
import Notifications from 'material-ui/svg-icons/social/notifications';
import IconButton from 'material-ui/IconButton';

import inlineStyles from './NavigationBarStyles';
import sentences from '../lang/index';

class NavigationBar extends React.Component {

  static propTypes = {
    match: PropTypes.object.isRequired,
    location: PropTypes.object.isRequired,
    history: PropTypes.object.isRequired,
    name: PropTypes.object.isRequired,
  }

  render() {
    const { match, location, history, appName } = this.props

    return (
      <AppBar
        showMenuIconButton={false}
        title={ appName }
        style={inlineStyles.appBar.root}
        titleStyle={inlineStyles.appBar.title}
        onTitleClick={()=> history.push('/')}
        zDepth={0}
        iconStyleRight={inlineStyles.appBar.elementRight}
        iconElementRight={
          <div>
            <IconButton
              name="sign-out-button"
              disableTouchRipple={true}
              onClick={()=> history.push('/search')}
            >
              <FindInPage color={inlineStyles.iconColor} />
            </IconButton>

            <IconMenu
              iconButtonElement={
                <IconButton name="about-button" disableTouchRipple={true} >
                  <Notifications color={inlineStyles.iconColor} />
                </IconButton>
              }
              anchorOrigin={{horizontal: 'left', vertical: 'bottom'}}
              targetOrigin={{horizontal: 'left', vertical: 'top'}}
            >
              <Link to="/new-users" >
                <MenuItem primaryText={sentences.UserCreations} />
              </Link>
              <Link to="/reported-publications" >
                <MenuItem primaryText={sentences.PostReports} />
              </Link>
            </IconMenu>

            <IconMenu
              iconButtonElement={
                <IconButton name="about-button" disableTouchRipple={true} >
                  <SocialPerson color={inlineStyles.iconColor} />
                </IconButton>
              }
              anchorOrigin={{horizontal: 'left', vertical: 'bottom'}}
              targetOrigin={{horizontal: 'left', vertical: 'top'}}
            >
              <Link to="/sign-in" >
                <MenuItem primaryText={sentences.signIn} />
              </Link>
              <Link to="/sign-out" >
                <MenuItem primaryText={sentences.signOut} />
              </Link>
              <Link to="/profile" >
                <MenuItem primaryText={sentences.profile} />
              </Link>
            </IconMenu>

            <IconMenu
              iconButtonElement={
                <IconButton name="about-button" disableTouchRipple={true} >
                  <Settings color={inlineStyles.iconColor} />
                </IconButton>
              }
              anchorOrigin={{horizontal: 'left', vertical: 'bottom'}}
              targetOrigin={{horizontal: 'left', vertical: 'top'}}
            >
              <Link to="/languages" >
                <MenuItem primaryText={sentences.languages} />
              </Link>
              <Link to="/fonts" >
                <MenuItem primaryText={sentences.fonts} />
              </Link>
            </IconMenu>
          </div>
        }
      />
  )}
}

export default withRouter(NavigationBar);