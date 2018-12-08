from application.db import db

class RevokedToken(db.Model):
  __tablename__ = 'revoked_tokens'
  
  id = db.Column(db.Integer, primary_key=True)
  jti = db.Column(db.String(120))

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def is_jti_blacklisted(cls, jti):
    return bool(cls.query.filter_by(jti=jti).first())
