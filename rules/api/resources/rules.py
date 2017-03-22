import logging
import re
from flask_restful import Resource
from common.auth0 import Auth0
from config import USER_DOMAIN, TOKEN_URL, TOKEN_INFO
from flask_restful.utils import cors
from flask.json import jsonify


class Rules(Resource):
    CLIENTS_URL = USER_DOMAIN + '/api/v2/clients'
    RULES_URL = USER_DOMAIN + '/api/v2/rules'

    @cors.crossdomain(origin='*')
    def get(self):
        auth0 = Auth0(TOKEN_URL, TOKEN_INFO)
        clients = Rules.get_clients(auth0)
        rules = Rules.get_rules(auth0)
        client_rules = Rules.get_client_rules(clients, rules)
        # Create dict for rules
        rules = {rule['id']: rule['name'] for rule in rules}
        # Can't serialize set to JSON, so convert to list first
        client_rules = {client: list(rules) for client, rules in client_rules.items()}
        
        logging.info('Clients: %s' % str(clients))
        logging.info('Rules: %s' % str(rules))
        logging.info('Client rules: %s' % str(client_rules))
        
        return jsonify({
            'clients': clients,
            'rules': rules,
            'client_rules': client_rules
        })

    @staticmethod
    def get_clients(auth0):
        clients = auth0.authorized_get(Rules.CLIENTS_URL)
        id_names = {client['client_id']: client['name'] for client in clients}
        return id_names

    @staticmethod
    def get_rules(auth0):
        return auth0.authorized_get(Rules.RULES_URL)

    @staticmethod
    def get_client_ids_from_rule(script):
        r = re.compile(r"context\.clientId\s*\!?===?\s*'([\w\s]+)'")
        return set(r.findall(script))

    @staticmethod
    def get_client_names_from_rule(script):
        r = re.compile(r"context\.clientName\s*\!?===?\s*'([\w\s]+)'")
        return set(r.findall(script))

    @staticmethod
    def extract_from_rule(script, id_names):
        client_ids = Rules.get_client_ids_from_rule(script)
        client_names = Rules.get_client_names_from_rule(script)

        if not client_ids and not client_names:
            return None

        names_ids = {v: k for k, v in id_names.items()}
        for name in client_names:
            if name in names_ids:
                client_ids.add(names_ids[name])
            else:
                logging.info('Unknown application: ' + name)

        return client_ids

    @staticmethod
    def get_client_rules(clients, rules):
        client_rules = {}
        for rule in rules:
            client_ids = Rules.extract_from_rule(rule['script'], clients)
            for client in client_ids:
                if client not in client_rules:
                    client_rules[client] = set()
                client_rules[client].add(rule['id'])
        return client_rules
