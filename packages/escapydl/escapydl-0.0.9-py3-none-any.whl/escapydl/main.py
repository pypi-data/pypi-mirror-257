# eSCAPyDL - a Deep Learning Side-Channel Analysis Python Framework
# Copyright (C) 2023  Weissbart Léo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os,sys
os.environ['GDK_BACKEND'] = 'x11'
import datetime
import logging
logging.basicConfig(format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import signal
import shlex
import argparse
import time
import subprocess

def main():
    #Parse arguments
    #TODO: remove default dataset and model and default to help
    parser = argparse.ArgumentParser(description='eSCAPyDL: Deep Leaning SCA PyTorch framework. Training models for tracesets with SCA metrics.')
    parser.add_argument('-d', '--dataset', help='The dataset to use for training. (All datasets have different functions for intermediate value and power model).', default="dpav4")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--train', help='Train the model', action='store_true')
    group.add_argument('-o', '--optimize', help='Optimize the model', action='store_true')
    parser.add_argument('-m', '--model', help='Type of NN to use (choices: MLP, CNN) CNN is the onetrace implementation', default="MLP")
    parser.add_argument('-s', '--study', help='Optuna study name, for parallelization of study')
    parser.add_argument('-u', '--database', help='Optuna database name', default="sqlite:///cnn_sca.db")
    parser.add_argument('-g', '--gui', help='Start graphical interface', action='store_true', default=False)
    parser.add_argument('-j', '--json', help='Input data from json file')
    parser.add_argument('-a', '--timestamp', help='Timestamp of the experiment', default=time.strftime("%Y%m%d_%H%M%S",time.localtime()))
    parser.add_argument('-v', '--verbose', help='Verbose level', action='count', default=0)
    parser.add_argument('-l', '--log', help='Log into a file at path', default='')
    args = parser.parse_args()
    if args.verbose == 1:
        logger.setLevel(logging.DEBUG)
    if args.log != '':
        file_handler = logging.FileHandler(args.log, mode='w', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S'))
        logger.addHandler(file_handler)
    if args.train == False and args.optimize == False:
        args.train = True

    logger.debug(args)
    if args.gui:
        command = sys.executable + " {} -l '{}'".format(os.path.join(os.path.dirname(__file__), "gui.py"), args.log)
    else:
        if args.train:
            command = sys.executable + " {} -d {} -m {} -j {} -a {}".format(os.path.join(os.path.dirname(__file__), "train.py"), args.dataset, args.model, args.json, args.timestamp)
        elif args.optimize:
            command = sys.executable + " {} -d {} -m {} -j {} -a {} -s {} -u {}".format(os.path.join(os.path.dirname(__file__),  "optimize.py"), args.dataset, args.model, args.json, args.timestamp, args.study, args.database)
        else:
            logger.error("Error: No action specified. Use '-t' to start straining or '-o' to start optimization")
            exit(1)
    if args.verbose > 0:
        command += " -v"
    logging.debug("Command: {}".format(command))
    #Run command
    p_args = shlex.split(command)
    try:
        start_time = datetime.datetime.now().replace(microsecond=0)
        process = subprocess.Popen(p_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logger.debug("Process {} started".format(process.pid))
        while process.poll() is None:
            log_out = process.stdout.readline().decode('utf-8').strip()
            if log_out != '':
                logger.info(log_out)
        logger.debug("Process {} done".format(process.pid))
        stop_time = datetime.datetime.now().replace(microsecond=0)
        if not args.gui:
            logger.info("----------------------\n  The operation was \ncompleted successfully\n Clear time {}\n----------------------".format(stop_time-start_time))
    except KeyboardInterrupt:
        logger.warning("Got Keyboard interrupt")
        logger.debug("Killing process {}".format(process.pid))
        process.send_signal(signal.SIGINT)
        while process.poll() is None:
            log_out = process.stdout.readline().decode('utf-8').strip()
            if log_out != '':
                logger.info(log_out)
    except Exception as e:
        logger.warning(e)
    logger.debug("Program Exited")
    
if __name__ == "__main__":
    sys.exit(main())