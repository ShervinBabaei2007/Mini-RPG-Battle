from main import Enemy, Player, WhiteTiger


def test_level_up():
    p = Player("Hero")
    p.level_up(250)
    assert p.level == 1


def test_take_damage_no_negative_hp():
    e = Enemy()
    e.take_damage(9999)
    assert e.hp == 0


def test_boss_enrages_at_half_hp():
    boss = WhiteTiger()
    damage_to_half = boss.max_hp // 2

    boss.take_damage(damage_to_half)

    assert boss.enraged is True
    assert boss.attack_power > 25
