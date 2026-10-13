// Prevent Chaos Robes from being equipped on dragonflies
// This fixes the ClassCastException crash between Soul Weaponry and Critters & Companions

ServerEvents.tick((event) => {
  // Only run once per second to reduce lag
  if (event.server.tickCount % 20 !== 0) return;

  event.server.level
    .getEntities("@e[type=crittersandcompanions:dragonfly]")
    .forEach((dragonfly) => {
      let armor = dragonfly.getArmor();

      // Check if dragonfly is wearing Chaos Robes
      if (armor.isEmpty()) return;

      // Drop Chaos Robes if equipped
      if (
        armor.getTag() === "soulsweapons:chaos_robes" ||
        armor.id === "soulsweapons:chaos_robes" ||
        armor.getItem().match("*chaos_robes*")
      ) {
        // Drop the armor and remove from entity
        dragonfly.drop(armor);
        dragonfly.setArmor(null);
      }
    });
});
