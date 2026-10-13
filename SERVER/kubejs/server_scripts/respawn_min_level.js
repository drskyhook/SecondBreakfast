PlayerEvents.respawned(event => {
  const p = event.player;

  if (p.experienceLevel < 1) {
    p.experienceLevel = 1
  }
})