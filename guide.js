// Keep the article, example frames and downloads usable without JavaScript.
const explorer = document.querySelector('[data-exposure-explorer]');
if (explorer) {
  const shutter = ['1.3 s', '1 s', '0.6 s', '0.4 s', '1/4 s', '1/5 s', '1/8 s', '1/13 s', '1/20 s', '1/30 s', '1/50 s'];
  const slider = document.getElementById('exposure-range');
  const photo = document.getElementById('exposure-image');
  const update = () => {
    const index = Number(slider.value);
    const frame = String(418 + index).padStart(4, '0');
    photo.src = `assets/tutorial/fisheye-${frame}.webp`;
    photo.alt = `Example fisheye exposure IMG_${frame}.JPG at ${shutter[index]}`;
    document.getElementById('exposure-label').textContent = `IMG_${frame}.JPG · ${shutter[index]} · f/4 · ISO 200`;
    document.getElementById('exposure-position').textContent = `${index + 1} / ${shutter.length}`;
    slider.setAttribute('aria-valuetext', `${shutter[index]}, frame ${index + 1} of ${shutter.length}`);
  };
  slider.addEventListener('input', update);
  update();
  explorer.hidden = false;
}
