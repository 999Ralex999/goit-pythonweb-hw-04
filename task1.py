import asyncio
import logging
from argparse import ArgumentParser
from aiopath import AsyncPath
from aioshutil import copy as async_copy

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def copy_file(file: AsyncPath, output_dir: AsyncPath):
    try:
        ext = file.suffix[1:] if file.suffix else 'no_extension'
        target_dir = output_dir / ext

        if not await target_dir.exists():
            await target_dir.mkdir(parents=True, exist_ok=True)

        target_file = target_dir / file.name
        counter = 1
        while await target_file.exists():
            new_name = f"{file.stem}_{counter}{file.suffix}"
            target_file = target_dir / new_name
            counter += 1

        await async_copy(file, target_file)
        logging.info(f"✅ {file} успішно скопійовано до {target_file}")

    except Exception as e:
        logging.error(f"❌ Помилка під час копіювання {file}: {e}")

async def read_and_copy(source_dir: AsyncPath, output_dir: AsyncPath):
    if not await source_dir.exists():
        logging.error(f"❌ Вихідна папка {source_dir} не існує")
        return

    tasks = []
    async for path in source_dir.glob("**/*"):
        if await path.is_file():
            tasks.append(copy_file(path, output_dir))

    await asyncio.gather(*tasks)

def main():
    parser = ArgumentParser(description="Асинхронне сортування файлів за розширенням")
    parser.add_argument("source", type=str, help="Шлях до вихідної папки")
    parser.add_argument("output", type=str, help="Шлях до папки призначення")
    args = parser.parse_args()

    source_dir = AsyncPath(args.source)
    output_dir = AsyncPath(args.output)

    asyncio.run(read_and_copy(source_dir, output_dir))

if __name__ == "__main__":
    main()

