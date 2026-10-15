from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os
from collections import deque
from datetime import datetime
app=Flask(__name__); app.secret_key=os.environ.get("SECRET_KEY","dev-only-change-me")
DB=os.path.join(os.path.dirname(__file__),"foodflow.db")
MENU=[{"id":1,"name":"Classic Margherita","desc":"Tomato, mozzarella and basil","category":"Pizza","emoji":"🍕","price":249},{"id":2,"name":"Crispy Fries","desc":"Golden, lightly seasoned fries","category":"Sides","emoji":"🍟","price":99},{"id":3,"name":"Garden Burger","desc":"Veg patty, greens and house sauce","category":"Burgers","emoji":"🍔","price":179},{"id":4,"name":"Choco Shake","desc":"Creamy chocolate milkshake","category":"Drinks","emoji":"🥤","price":129},{"id":5,"name":"Paneer Wrap","desc":"Spiced paneer with crunchy salad","category":"Wraps","emoji":"🌯","price":159},{"id":6,"name":"Brownie Bite","desc":"Warm chocolate brownie","category":"Dessert","emoji":"🍫","price":89}]
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
 with db() as c: c.execute("CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,customer TEXT NOT NULL,items TEXT NOT NULL,total INTEGER NOT NULL,status TEXT NOT NULL,created_at TEXT NOT NULL)")
init_db()
def get_orders():
 with db() as c: rows=c.execute("SELECT * FROM orders ORDER BY id").fetchall()
 return [dict(r) for r in rows]
def queue_ids():
 return deque(o["id"] for o in get_orders() if o["status"] not in ("Completed","Cancelled"))
@app.get("/")
def index(): return render_template("index.html",menu=MENU)
@app.post("/order")
def order():
 customer=request.form.get("customer","").strip()
 try: quantities=[int(x) for x in request.form.getlist("quantity")]
 except ValueError: quantities=[]
 selected=[]
 for item,q in zip(MENU,quantities):
  if 0<q<=20: selected.append((item,q))
 if not customer or not selected:
  flash("Enter your name and select at least one item."); return redirect(url_for("index"))
 items=", ".join(f"{q} × {item['name']}" for item,q in selected); total=sum(item["price"]*q for item,q in selected)
 with db() as c: c.execute("INSERT INTO orders(customer,items,total,status,created_at) VALUES(?,?,?,?,?)",(customer,items,total,"Received",datetime.now().isoformat(timespec="minutes")))
 flash("Order placed and added to the FIFO queue."); return redirect(url_for("orders"))
@app.get("/orders")
def orders(): return render_template("orders.html",orders=get_orders(),queue=queue_ids())
@app.post("/orders/<int:oid>/status")
def update_status(oid):
 status=request.form.get("status","")
 if status not in ("Received","Preparing","Ready","Completed","Cancelled"): status="Received"
 with db() as c: c.execute("UPDATE orders SET status=? WHERE id=?",(status,oid))
 return redirect(url_for("orders"))
@app.get("/health")
def health(): return {"status":"ok","app":"FoodFlow"}
if __name__=="__main__": app.run(debug=True)
