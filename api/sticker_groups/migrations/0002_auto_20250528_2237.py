from django.db import migrations


def add_sticker_groups(apps, schema_editor):
    StickerGroup = apps.get_model("sticker_groups", "StickerGroup")
    groups = [
        "[FWC] Especiais",
        "[FWC] Estádios",
        "[FWC] Bola",
        "[QAT] Catar",
        "[ECU] Equador",
        "[SEN] Senegal",
        "[NED] Holanda",
        "[ENG] Inglaterra",
        "[IRN] Irã",
        "[USA] Estados Unidos",
        "[WAL] País de Gales",
        "[ARG] Argentina",
        "[KSA] Arábia Saudita",
        "[MEX] Mexico",
        "[POL] Polônia",
        "[FRA] França",
        "[AUS] Austrália",
        "[DEN] Dinamarca",
        "[TUN] Tunísia",
        "[ESP] Espanha",
        "[CRC] Costa Rica",
        "[GER] Alemanha",
        "[JPN] Japão",
        "[BEL] Bélgica",
        "[CAN] Canadá",
        "[MAR] Marrocos",
        "[CRO] Croácia",
        "[BRA] Brasil",
        "[SRB] Sérvia",
        "[SUI] Suíça",
        "[CMR] Camarões",
        "[POR] Portugal",
        "[GHA] Gana",
        "[URU] Uruguai",
        "[KOR] Coreia do Sul",
    ]

    for group_name in groups:
        StickerGroup.objects.get_or_create(name=group_name)


class Migration(migrations.Migration):
    dependencies = [
        ("sticker_groups", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_sticker_groups),
    ]
