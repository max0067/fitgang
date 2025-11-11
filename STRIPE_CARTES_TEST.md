# Cartes de test Stripe

## Cartes de test principales

### ✅ Paiement réussi
```
Numéro: 4242 4242 4242 4242
Date: N'importe quelle date future (ex: 12/34)
CVC: N'importe quel 3 chiffres (ex: 123)
Code postal: N'importe lequel
```

### ❌ Paiement refusé
```
Numéro: 4000 0000 0000 0002
Date: 12/34
CVC: 123
```

### 🔒 Authentification 3D Secure requise
```
Numéro: 4000 0027 6000 3184
Date: 12/34
CVC: 123
```
Lors du paiement, Stripe affichera un modal de test 3D Secure.

### ⏳ Paiement en attente
```
Numéro: 4000 0000 0000 3220
Date: 12/34
CVC: 123
```

## Cartes internationales

### 🇪🇺 Carte européenne (standard)
```
Numéro: 4242 4242 4242 4242
```

### 🇺🇸 Carte américaine
```
Numéro: 4000 0056 6555 3573
```

### 🇬🇧 Carte britannique
```
Numéro: 4000 0082 6000 0000
```

## Erreurs spécifiques

### Carte expirée
```
Numéro: 4000 0000 0000 0069
```

### Carte avec code CVC invalide
```
Numéro: 4000 0000 0000 0127
```

### Fonds insuffisants
```
Numéro: 4000 0000 0000 9995
```

### Carte perdue/volée
```
Numéro: 4000 0000 0000 9987
```

## Comment tester

1. Va sur https://fitgang.fr (en mode TEST)
2. Connecte-toi avec un compte utilisateur
3. Choisis un programme ou ebook à acheter
4. Clique sur "Acheter"
5. Sur la page Stripe Checkout, utilise une des cartes ci-dessus
6. Entre les informations demandées
7. Valide le paiement

## Vérifier les paiements

### Dans le dashboard Stripe
- Va sur https://dashboard.stripe.com/test/payments
- Tu verras tous les paiements de test

### Dans FitGang
- Le paiement apparaîtra dans `/admin` (statistiques)
- L'utilisateur verra le produit dans son dashboard
- Un email de confirmation sera envoyé (si configuré)

## Montants de test

Tu peux utiliser n'importe quel montant avec les cartes de test:
- 0.50€ à 999999.99€
- Stripe ne prélèvera RIEN en mode TEST
- Tous les paiements sont simulés

## Webhooks en mode TEST

Les webhooks fonctionnent également en mode TEST:
- Configure un endpoint de test
- Stripe enverra des événements de test
- Tu peux simuler manuellement des webhooks depuis le dashboard

## Documentation complète

- https://stripe.com/docs/testing
- https://stripe.com/docs/testing/cards-wallets
