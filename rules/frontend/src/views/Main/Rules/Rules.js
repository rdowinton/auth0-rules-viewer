import React, { PropTypes as T } from 'react'
import AuthService from 'utils/AuthService'
import {Button} from 'react-bootstrap'
import styles from './styles.module.css'
import axios from 'axios'

export class Rules extends React.Component {
    RULES_BASE_URL = 'https://manage.auth0.com/#/rules/';
    CLIENTS_BASE_URL = 'https://manage.auth0.com/#/clients/';

    static contextTypes = {
        router: T.object
    }

    static propTypes = {
        auth: T.instanceOf(AuthService)
    }

    constructor(props, context) {
        super(props, context);
        this.state = {
            rules: [],
            clients: {},
            client_rules: {}
        };
    }

    componentDidMount() {
        var _this = this;
        this.apiRequest = axios.get('http://localhost/api/rules').then(function(result) {
            console.log(result.data);
            _this.setState({
                rules: result.data['rules'],
                clients: result.data['clients'],
                client_rules: result.data['client_rules']
            });
        });
    }

    componentWillUnmount() {
        this.apiRequest.abort()
    }

    logout() {
        this.props.auth.logout()
        this.context.router.push('/login');
    }

    render() {
        return (
            <div className={styles.root}>
                <h2>Application Rules</h2>
                <table className={styles.application_rules}>
                <tbody>
                {Object.keys(this.state.clients).map(client_id => {
                    var rules;
                    if(client_id in this.state.client_rules) {
                        rules = <ul className={styles.rules}>{
                            this.state.client_rules[client_id].map(rule_id => {
                                return (<li className={styles.rule_name} key={rule_id}>
                                    <a href={this.RULES_BASE_URL + rule_id}>{this.state.rules[rule_id]}</a>
                                </li>)
                            })}
                        </ul>
                    } else {
                        rules = <span>No rules</span>
                    }
                    return (
                        <tr className={styles.application_row} key={client_id}>
                        <td>
                        <a href={this.CLIENTS_BASE_URL + client_id}>{this.state.clients[client_id]}</a>
                        </td>
                        <td>
                        {rules}
                        </td>
                        </tr>
                    );
                })}
                </tbody>
                </table>
                <Button onClick={this.logout.bind(this)}>Logout</Button>
            </div>
        )
    }
}

export default Rules;