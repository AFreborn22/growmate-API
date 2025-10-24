from app.schemas.agent import ChatResponse
from app.schemas.user import InternalServerError

chat = {
    200: {
        "description": "Chatbot response successfully generated.",
        "model": ChatResponse,
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "Contoh respons sukses dari MateBot",
                        "value": {
                            "answer": "Halo Bunda, ada yang bisa MateBot bantu?",
                            "source_documents": [
                                {
                                    "content": (
                                        "Stunting adalah gangguan pertumbuhan dan perkembangan anak balita "
                                        "(di bawah lima tahun) yang ditandai dengan tinggi badan lebih rendah "
                                        "dari standar usianya karena kekurangan gizi kronis dan infeksi berulang."
                                    ),
                                    "metadata": {
                                        "id": "gizi_001",
                                        "source": "Kementerian Kesehatan RI",
                                        "topic": "Stunting",
                                        "sub_topic": "Definisi",
                                        "date_updated": "2024-09-01"
                                    }
                                },
                                {
                                    "content": (
                                        "Penyebab stunting dari segi gizi meliputi: Kekurangan kalori, protein, "
                                        "dan mikronutrien penting seperti zat besi, vitamin A, dan yodium."
                                    ),
                                    "metadata": {
                                        "id": "gizi_002",
                                        "source": "Jurnal Gizi Indonesia",
                                        "topic": "Stunting",
                                        "sub_topic": "Penyebab Gizi",
                                        "date_updated": "2024-08-15"
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error.",
        "model": InternalServerError,
        "content": {
            "application/json": {
                "examples": {
                    "ServerError": {
                        "summary": "Contoh kesalahan internal server",
                        "value": {"detail": "Terjadi kesalahan internal saat memproses query."}
                    }
                }
            }
        }
    }
}
