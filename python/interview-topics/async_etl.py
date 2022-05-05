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


class ETL:
    @staticmethod
    async def run():
        etl = ETL()
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
            print("Task #{}: {}".format(n + 1, task.get_name()))
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
    etl = ETL()

    print('Extract...')
    responses = await etl.extract()

    print('Transform...')
    data = await etl.transform(responses)

    print('Load...')
    result = etl.load(data)

    async_time = time.time() - started_at
    sync_time = sum([r.delay for r in responses])
    savings = ((sync_time / async_time) - 1) * 100
    result_f = 'Async (Actual) vs Sync Time: {:.2f} vs {:.2f} ({:.1f}%)'
    print('ETL result {}: {}'.format(data, result))
    print(result_f.format(async_time, sync_time, savings))


asyncio.run(main())
