import asyncio
import random
import time


class Response:
    STATUSES = ['ok', 'error']

    def __init__(self):
        self.started_at = time.time()
        self.load_delay = random.randint(1, 2000) / 1000
        self.transform_delay = random.randint(1, 500) / 1000
        self.status = random.choice(self.STATUSES)

        if self.status == 'ok':
            self.data = self.query_data()
        else:
            self.data = 'error'

    def query_data(self):
        return random.randint(1, 1000)

    def __repr__(self):
        f = '<Response started={} delays=({},{}) status={} data={}>'
        t1, t2 = str(self.started_at).split('.')
        started = '{}.{}'.format(t1[-3:], t2[:3])
        return f.format(started, self.load_delay, self.transform_delay, self.status, self.data)


class Extract:
    @staticmethod
    async def run():
        etl = Extract()
        responses = await etl.extract()
        data = await etl.transform(responses)
        return etl.load(data)

    async def extract(self):
        data = []

        for n in range(10):
            response = Response()
            await asyncio.sleep(response.load_delay)
            print("Response #{}: {}".format(n, response))
            data.append(response)

        return data

    async def transform(self, responses):
        data = []

        for response in responses:
            if response.status == 'ok':
                print("Transform: {}".format(response))
                await asyncio.sleep(response.transform_delay)
                data.append(response.data)
            else:
                print("Skip error: {}".format(response))

        return data

    def load(self, data):
        return sum(data)


async def main():
    print('Start extract run')
    result = await Extract.run()
    print('ETL result: {}'.format(result))

asyncio.run(main())
