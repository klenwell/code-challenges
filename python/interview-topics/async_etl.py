import asyncio
import random
import time


class Response:
    STATUSES = ['ok', 'error']

    def __init__(self):
        self.started_at = time.time()
        self.delay = random.randint(1, 2000) / 1000
        self.status = random.choice(self.STATUSES)

        if self.status == 'ok':
            self.data = self.query_data()
        else:
            self.data = 'error'

    def query_data(self):
        return random.randint(1, 1000)

    def __repr__(self):
        f = '<Response started={} delay={} status={} data={}>'
        t1, t2 = str(self.started_at).split('.')
        started = '{}.{}'.format(t1[-3:], t2[:3])
        return f.format(started, self.delay, self.status, self.data)


class Extract:
    @staticmethod
    async def run():
        etl = Extract()
        responses = await etl.extract()
        data = await etl.transform(responses)
        return etl.load(data)

    async def request_data(self):
        response = Response()
        await asyncio.sleep(response.delay)
        return response

    async def extract(self):
        responses = []
        tasks = []

        for n in range(10):
            await asyncio.sleep(0.2)
            task = asyncio.create_task(self.request_data())
            print("Task #{}: {}".format(n, task.get_name()))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses

    async def transform(self, responses):
        data = []

        for response in responses:
            if response.status == 'ok':
                print("Transform: {}".format(response))
                data.append(response.data)
            else:
                print("Skip error: {}".format(response))

        return data

    def load(self, data):
        return sum(data)


async def main():
    print('Start ETL')
    started_at = time.time()
    etl = Extract()

    print('Extract...')
    responses = await etl.extract()

    print('Transform...')
    data = await etl.transform(responses)

    print('Load...')
    result = etl.load(data)

    run_time = time.time() - started_at
    delays = sum([r.delay for r in responses])
    print('ETL result {}: {}'.format(data, result))
    print('Run Time vs Request Delays: {:.2f} / {:.2f}'.format(run_time, delays))


asyncio.run(main())
