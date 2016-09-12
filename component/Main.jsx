'use strict';
/**
 * Created by FrankTsai on 2016/7/6.
 */
import React from 'react';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import LinearProgress from 'material-ui/LinearProgress';
import Select from 'react-select';

// Be sure to include styles at some point, probably during your bootstrapping
import 'react-select/dist/react-select.css';

const styles = {
  container: {
    width: '100%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '15px',
  },
  formContainer: {
    width: 'auto'
  },
  input: {
    marginTop: '5px',
    display: 'block',
  }
}
export default class Nav extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      captcha: '',
      account: '',
      password: '',
      auth_num: '',
      course_id: '',
      result: '',
      chooseCourse: {},
      courses: [],
    }
    this.getCaptcha = this.getCaptcha.bind(this);
    this.getCourse = this.getCourse.bind(this);
    this.submit = this.submit.bind(this);
    this.handleSelect = this.handleSelect.bind(this);
  }
  componentDidMount() {
    this.getCaptcha();
    this.getCourse();
  }
  handleSelect(val) {
    this.setState({chooseCourse: val});
  }
  submit() {
    const { account, password, auth_num, chooseCourse } = this.state;
    this.setState({loading: true})
    const data = {
      account,
      password,
      auth_num,
      course_id: chooseCourse.value,
      real: chooseCourse.real,
    }
    $.ajax({
      method: 'POST',
      url: '/api/choose/',
      data,
    })
      .done(
        response => this.setState({result: response.result, loading: false})
      )
  }
  getCaptcha() {
    $.ajax({
      url: '/api/captcha',
      method: 'GET',
    })
      .done(
        response => this.setState({captcha: response.captcha})
      )
  }
  getCourse() {
    $.ajax({
      url: '/api/course',
      method: 'GET',
    })
      .done(
        response => this.setState({courses: response.courses[0]})
      )
  }
  render() {
    const response = this.state.result === 'success' ? <h1>選到了，修課愉快</h1> : 
          <h1>{this.state.result}</h1>;
    return (
      <div>
      { this.state.result.length > 0 ? <section className="web-container" style={styles.container}>
        <div className="form" style={styles.formContainer}>
          {response}
        </div>
      </section> :
      <section className="web-container" style={styles.container}>
        <div className="form" style={styles.formContainer}>
          { this.state.loading ? <LinearProgress mode="indeterminate" /> : '' } 
          <TextField
            floatingLabelText="Account"
            onChange={(e) => this.setState({account: e.target.value})}
            style={styles.input}
          />
          <TextField 
            floatingLabelText="Password"
            type="password"
            onChange={(e) => this.setState({password: e.target.value})}
            style={styles.input}
          />
          <TextField
            floatingLabelText="Captcha"
            onChange={(e) => this.setState({auth_num: e.target.value})}
            style={styles.input}
          />
          { this.state.captcha === '' ? '' : <img src={`/static/captcha/${this.state.captcha}`} /> }
          <Select
              value={this.state.chooseCourse}
              options={this.state.courses}
              onChange={this.handleSelect}
          />
          <RaisedButton 
            label="拜託選到" 
            primary={true} 
            onClick={this.submit}
            style={styles.input}
          />
        </div>
      </section>
      }
      </div>
    )
  }
}
