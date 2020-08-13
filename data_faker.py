import sys
import random

from backend.engine.watcher import Watcher
from backend.engine import datastore
from backend.engine import snapper


def fake_field(date, date_str, name, value):
    if name == 'date':
        return date_str
    if name == 'date_components':
        return date
    if isinstance(value, str) or isinstance(value, int):
        return value
    if isinstance(value, dict):
        return fake_dict(date, date_str, value)
    if isinstance(value, list):
        return [
            fake_field(date, date_str, v) for v in value
        ]
    pchg = random.randint(-3, 8) / 100 + 1
    return value * pchg


def fake_dict(date, date_str, snap):
    return {
        name: fake_field(date, date_str, name, value)
        for name, value in snap.items()
    }


def fake_snap(snap):
    date = snapper._parse_date(snap['date'])
    date['m'] += 1
    if date['m'] >= 13:
        date['m'] = 1
        date['y'] += 1
    date_str = f'{date["y"]}.{date["m"]}.{date["d"]}'
    return {
        'date': date_str,
        'empires': {
            eid: fake_dict(date, date_str, empire)
            for eid, empire in snap['empires'].items()
        }
    }


def main():
    if len(sys.argv) != 3:
        print('USAGE: data_faker.py <save_folder> <months to add>')
    folder = sys.argv[1]
    steps = int(sys.argv[2])

    watcher = Watcher(folder)
    if not watcher.valid:
        print(f'Invalid Stellaris save: {folder}')
    
    print('Loading save and building snapshot')
    snap = snapper.build_snapshot_from_watcher(watcher)

    print(f'Creating {steps} extra months of data')
    snaps = [snap]
    for i in range(0, steps):
        snaps.append(fake_snap(snaps[-1]))

    print(f'Saving new data')
    datastore._flush_save({'snaps': snaps, 'directory': folder})


if __name__ == '__main__':
    main()
