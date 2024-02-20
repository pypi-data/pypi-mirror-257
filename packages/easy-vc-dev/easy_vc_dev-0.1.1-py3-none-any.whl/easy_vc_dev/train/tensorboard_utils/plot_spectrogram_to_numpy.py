import logging

MATPLOTLIB_FLAG = False


def plot_spectrogram_to_numpy(spectrogram):
    global MATPLOTLIB_FLAG
    if not MATPLOTLIB_FLAG:
        import matplotlib

        matplotlib.use("Agg")
        MATPLOTLIB_FLAG = True
        mpl_logger = logging.getLogger("matplotlib")
        mpl_logger.setLevel(logging.WARNING)
    import matplotlib.pylab as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(10, 2))
    im = ax.imshow(spectrogram, aspect="auto", origin="lower", interpolation="none")
    plt.colorbar(im, ax=ax)
    plt.xlabel("Frames")
    plt.ylabel("Channels")
    plt.tight_layout()

    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep="")
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close()
    return data


def plot_2spectrogram_to_numpy(spectrogram1, spectrogram2):
    global MATPLOTLIB_FLAG
    if not MATPLOTLIB_FLAG:
        import matplotlib

        matplotlib.use("Agg")
        MATPLOTLIB_FLAG = True
        mpl_logger = logging.getLogger("matplotlib")
        mpl_logger.setLevel(logging.WARNING)
    import matplotlib.pylab as plt
    import numpy as np

    fig, axs = plt.subplots(2, 1, figsize=(16, 8))  # 2行1列のサブプロット
    ax1, ax2 = axs

    # スペクトログラム1の描画
    im1 = ax1.imshow(spectrogram1, aspect="auto", origin="lower", interpolation="none")
    plt.colorbar(im1, ax=ax1)
    ax1.set(xlabel="Frames(org)", ylabel="Channels")

    # スペクトログラム2の描画
    im2 = ax2.imshow(spectrogram2, aspect="auto", origin="lower", interpolation="none")
    plt.colorbar(im2, ax=ax2)
    ax2.set(xlabel="Frames(gen)", ylabel="Channels")

    plt.tight_layout()  # レイアウトの調整

    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)  # fromstringからfrombufferへの修正
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close()
    return data
