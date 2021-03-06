#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import tensorflow as tf
from importlib import import_module
from utils import build_dataset, get_time_dif, build_net_data, save_file
import argparse
import os

parser = argparse.ArgumentParser(description='Chinese Text Classification')
parser.add_argument('--model', default="Bert", type=str,
                    help='choose a model: BruceBert, BruceBertCNN,BruceBertRNN')
args = parser.parse_args()

if __name__ == '__main__':
    dataset = 'News'  # 数据集
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    model_name = args.model  # 'Bert'
    x = import_module('models.' + model_name)  # 一个函数运行需要根据不同项目的配置，动态导入对应的配置文件运行。
    config = x.Config(dataset)  # 进入到对应模型的__init__方法进行参数初始化
    start_time = time.time()
    print("Loading data...")
    save_file(config)
    train_data, dev_data, test_data = build_dataset(config)
    time_dif = get_time_dif(start_time)
    print("Time usage:", time_dif)

    train_x, train_y = build_net_data(train_data, config)
    dev_x, dev_y = build_net_data(dev_data, config)
    test_x, test_y = build_net_data(test_data, config)

    # train
    model = x.MyModel(config)
    optimizer = tf.keras.optimizers.Adam(learning_rate=config.learning_rate)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(filepath=config.save_path, save_best_only=True, save_weights_only=True)
    ]
    history = model.fit(
        x=train_x,
        y=train_y,
        validation_data=(dev_x, dev_y),
        batch_size=8,
        epochs=30,
        callbacks=callbacks
    )