class ConversationSeparator:
    def separate(self, segments):
        agent, customer = [], []
        for i, seg in enumerate(segments):
            text = seg["text"].strip()
            if i % 2 == 0:
                agent.append(text)
            else:
                customer.append(text)
        return {"agent": " ".join(agent), "customer": " ".join(customer)}
