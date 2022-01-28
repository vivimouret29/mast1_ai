# TP SEGMENTATION

## Jeu de données

Composé de différentes photos de chats et de chiens.

## Utilisation de différents modèles

Pour commencer, différents model ont été utilisés :
```bash
Mobile_net_v2 185/185 [==============================] - 38s 207ms/step - loss: 0.0000e+00 - accuracy: 0.0517 - val_loss: 0.0000e+00 - val_accuracy: 0.0507

Inception_v3 185/185 [==============================] - 40s 217ms/step - loss: 0.0000e+00 - accuracy: 0.5686 - val_loss: 0.0000e+00 - val_accuracy: 0.5804

Resnet_50 185/185 [==============================] - 40s 214ms/step - loss: 0.0000e+00 - accuracy: 0.0451 - val_loss: 0.0000e+00 - val_accuracy: 0.0533
```

On peut voir que les scores des model n'ont pas bougé du tout, même après la première epoch. 
Les modèles avec la base Inception_v3 semblent être obtenir un meilleur rendu rapport aux autres model.
Je vais donc continuer avec Inception_v3

## Réalisation des XP

J'ai réalisé ces images depuis le notebook `segmentation_colab`:

- Description et paramètres d'une photo:  
![catdes](./readme/catdes.PNG)


- Suivi de la segmentation sur une photo modifiée:  
![catocat](./readme/catocat.PNG)

## Résultats

Ces deux prochains résultats sont issues de deux notebook différents :

- Exemple de résultat sous Inception_v4
![inception](./readme/inception.PNG)

- Et sous ResNet50
```bash
INFO:tensorflow:Calling model_fn.
ERROR:tensorflow:Operation of type Placeholder (input_1) is not supported on the TPU. Execution will fail if this op is used in the graph. 
/usr/local/lib/python3.6/dist-packages/keras_applications/resnet50.py:265: UserWarning:

The output shape of `ResNet50(include_top=False)` has been changed since Keras 2.2.0.

INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2019-05-23T16:33:37Z
INFO:tensorflow:TPU job name worker
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from gs://gs_colab/work/tutorial8/2019-05-23-16:28:08/model.ckpt-460
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Init TPU system
INFO:tensorflow:Initialized TPU in 10 seconds
INFO:tensorflow:Starting infeed thread controller.
INFO:tensorflow:Starting outfeed thread controller.
INFO:tensorflow:Initialized dataset iterators in 0 seconds
INFO:tensorflow:Enqueue next (1) batch(es) of data to infeed.
INFO:tensorflow:Dequeue next (1) batch(es) of data from outfeed.
INFO:tensorflow:Evaluation [1/1]
INFO:tensorflow:Stop infeed thread controller
INFO:tensorflow:Shutting down InfeedController thread.
INFO:tensorflow:InfeedController received shutdown signal, stopping.
INFO:tensorflow:Infeed thread finished, shutting down.
INFO:tensorflow:infeed marked as finished
INFO:tensorflow:Stop output thread controller
INFO:tensorflow:Shutting down OutfeedController thread.
INFO:tensorflow:OutfeedController received shutdown signal, stopping.
INFO:tensorflow:Outfeed thread finished, shutting down.
INFO:tensorflow:outfeed marked as finished
INFO:tensorflow:Shutdown TPU system.
INFO:tensorflow:Finished evaluation at 2019-05-23-16:34:01
INFO:tensorflow:Saving dict for global step 460: accuracy = 0.9089674, global_step = 460, loss = 0.29057366
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 460: gs://gs_colab/work/sample_data/2019-05-23-16:28:08/model.ckpt-460
INFO:tensorflow:evaluation_loop marked as finished
```

Globalement, ResNet a obtenu de meilleurs résultats par rapport à Inception_v4, malgrés mes tests du début.