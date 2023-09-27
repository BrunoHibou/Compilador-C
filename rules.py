import re
from token import Token, TokenClass


class RuleInterface:
    def regex_rules(self) -> list[str]:
        pass
    def extract_token(self, match: str) -> Token:
        pass
    def check_match(self, content: str) -> re.Match:
        for rule in self.regex_rules():
            match = re.match('^' + rule, content)
            if match:
                return match
        return None


class NumberConstantRule(RuleInterface):
    def regex_rule(self) -> list[str]:
        return ['[0-9]+', '[0-9]+.[0-9]+']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.NUMERICAL_CONSTANT, int(match))


class IdRule(RuleInterface):
    def regex_rule(self) -> list[str]:
        return ['[a-zA-Z_][a-zA-Z0-9_]*']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.ID, match)


class SymbolRule(RuleInterface):
    def regex_rule(self) -> list[str]:
        return ['\\{', '\\}', '\\(', '\\)', '\\+', '-', '\\*', '/']
    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.SYMBOL, match)