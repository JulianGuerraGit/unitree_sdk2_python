import sys
import time
import termios
import tty
import select

from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.g1.loco.g1_loco_client import LocoClient


def get_key(timeout: float = 0.1) -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            return sys.stdin.read(1)
        return ''
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} networkInterface")
        sys.exit(-1)

    print("WARNING: Please ensure there are no obstacles around the robot while running this example.")
    input("Press Enter to continue...")
    print(
        "Ensure the robot is placed facing up ready to stand from a laying position."
    )
    input("Press Enter to continue...")

    ChannelFactoryInitialize(0, sys.argv[1])

    loco = LocoClient()
    loco.SetTimeout(10.0)
    loco.Init()

    loco.Damp()
    time.sleep(0.5)
    loco.Lie2StandUp()

    print("Use WASD keys to move, Q/E to rotate. Press Ctrl+C to exit.")
    try:
        while True:
            key = get_key(0.1)
            vx = vy = vyaw = 0.0
            if key == 'w':
                vx = 0.3
            elif key == 's':
                vx = -0.3
            elif key == 'a':
                vy = 0.3
            elif key == 'd':
                vy = -0.3
            elif key == 'q':
                vyaw = 0.3
            elif key == 'e':
                vyaw = -0.3

            if key:
                loco.Move(vx, vy, vyaw)
            else:
                loco.StopMove()
    except KeyboardInterrupt:
        pass
    finally:
        loco.StopMove()


if __name__ == "__main__":
    main()
