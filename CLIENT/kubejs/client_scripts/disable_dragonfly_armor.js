// Disable armor rendering on dragonflies to prevent ClassCastException crashes
// Listens for render event instead of ticking

ClientEvents.registry("entity_renderer", (event) => {
  // Register a custom render handler for dragonflies
  event.register("crittersandcompanions:dragonfly", (context) => {
    let entity = context.entity;

    // Clear armor slots to prevent incompatible armor from being rendered
    if (entity && entity.getArmor && entity.getArmor()) {
      entity.setArmor(null);
    }
  });
});
