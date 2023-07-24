const getRandomColor = () => {
  let o = Math.round,
    r = Math.random,
    s = 255;
  return (
    "rgba(" +
    o(r() * s) +
    "," +
    o(r() * s) +
    "," +
    o(r() * s) +
    "," +
    0.9 +
    /* r().toFixed(1) */ ")"
  );
};

export { getRandomColor };
