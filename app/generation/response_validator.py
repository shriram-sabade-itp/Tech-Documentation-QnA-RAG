class ResponseValidator:

    def validate(self,
                 response_text):

        if not response_text:

            return False

        if len(response_text.strip()) == 0:

            return False

        return True