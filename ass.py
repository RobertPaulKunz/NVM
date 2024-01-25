import asyncio
import time


async def print_abc():
    print('A')
    await asyncio.sleep(2)
    print('B')
    await asyncio.sleep(2)
    print('C')
    
async def print_123():
    print('1')
    await asyncio.sleep(2)
    print('2')
    await asyncio.sleep(2)
    print('3')
    
async def print_xyz():
    print('X')
    await asyncio.sleep(2)
    print('Y')
    await asyncio.sleep(2)
    print('Z')

async def main():
    start_time = time.time()
#     task = asyncio.create_task(print_abc())
#     await print_123()
#     await print_xyz()
#     await task
    await asyncio.gather(print_123(), asyncio.wait_for(print_xyz(),5), print_abc())
    print('E')
    print('F')
    print(f'total time: {time.time() - start_time}')
    
asyncio.run(main())