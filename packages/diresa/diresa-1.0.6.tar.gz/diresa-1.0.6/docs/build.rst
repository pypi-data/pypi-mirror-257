.. _build:

*DIRESA* model
==============

**3. Build DIRESA model**

We can build a *DIRESA* model with convolutional and/or dense layers with the build_diresa function. 
We can also build a *DIRESA* model based on a custom encoder and decoder with the *diresa_model* function (see below). 
We build here a model with an input shape of *(3,)* for the 3D butterfly points. 
Our encoder model has 3 dense layers with 40, 20 and 2 units (the latter is the dimension of the latent space). 
The decoder is a reflection of the encoder. The DIRESA model has 3 loss functions, 
the reconstruction loss (usually the MSE is used here), the covariance loss and a distance loss 
(here the MSE distance loss is used). Also the weights for the diffenent loss functions are specified.

.. code-block:: ipython
  
  from diresa.models import build_diresa
  from diresa.loss import mse_dist_loss, LatentCovLoss

  diresa = build_diresa(input_shape=(3,), dense_units=(40, 20, 2))

  diresa.compile(loss=['MSE', LatentCovLoss(1.), mse_dist_loss], loss_weights=[1., 3., 1.])
  diresa.summary(expand_nested=True)
  
**4. Train the DIRESA model**

We train the *DIRESA* model in a standard way. The output of the decoder should fit the input of the encoder. 
The batch size should be large enough for the calculation of the covariance loss, which calculates 
the covariance matrix of the latent space components over the batch.

.. code-block:: ipython
  
  diresa.fit((train, train_twin), train, epochs=20, batch_size=512, shuffle=True, verbose=2)
  
**5. Encoder and decoder submodel**

We cut out the encoder and decoder submodels with the cut_sub_model function. 
So we can make predictions for latent and decoded space.

.. code-block:: ipython
  
  from diresa.toolbox import cut_sub_model
  compress_model = cut_sub_model(diresa, 'Encoder')
  decode_model = cut_sub_model(diresa, 'Decoder')
  latent = compress_model.predict(train)
  predict = decode_model.predict(latent)