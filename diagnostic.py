#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de diagnostic pour identifier le problème
"""
import sys
import traceback

print("=" * 60)
print("DIAGNOSTIC FITGANG")
print("=" * 60)

# Test 1: Import Flask
print("\n1. Test import Flask...")
try:
    from flask import Flask
    print("   ✓ Flask OK")
except Exception as e:
    print(f"   ✗ ERREUR Flask: {e}")
    sys.exit(1)

# Test 2: Import app
print("\n2. Test import create_app...")
try:
    from app import create_app
    print("   ✓ create_app OK")
except Exception as e:
    print(f"   ✗ ERREUR create_app: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 3: Création app
print("\n3. Test création application...")
try:
    app = create_app()
    print("   ✓ Application créée OK")
except Exception as e:
    print(f"   ✗ ERREUR création app: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 4: Test d'une route
print("\n4. Test route index...")
try:
    with app.test_client() as client:
        response = client.get('/')
        print(f"   Status code: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Route index OK")
        else:
            print(f"   ⚠ Status code: {response.status_code}")
except Exception as e:
    print(f"   ✗ ERREUR route: {e}")
    traceback.print_exc()

# Test 5: Test route admin
print("\n5. Test route admin...")
try:
    with app.test_client() as client:
        response = client.get('/admin', follow_redirects=False)
        print(f"   Status code: {response.status_code}")
        if response.status_code in [200, 302, 401]:
            print("   ✓ Route admin OK (redirection attendue)")
        else:
            print(f"   ✗ Status inattendu: {response.status_code}")
except Exception as e:
    print(f"   ✗ ERREUR route admin: {e}")
    traceback.print_exc()

print("\n" + "=" * 60)
print("FIN DU DIAGNOSTIC")
print("=" * 60)
